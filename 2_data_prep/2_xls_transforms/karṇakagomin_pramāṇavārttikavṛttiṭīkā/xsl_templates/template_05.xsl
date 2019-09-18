<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="p/quote[@sameAs]|l/quote[@sameAs]">
<xsl:text>"</xsl:text>
<xsl:value-of select="node()"/>
<xsl:text>"</xsl:text>
<xsl:text>(</xsl:text>
<xsl:value-of select="@sameAs"/>
<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="p/quote[@corresp]|l/quote[@corresp]">
<xsl:text>"</xsl:text>
<xsl:value-of select="node()"/>
<xsl:text>"</xsl:text>
<xsl:text>(</xsl:text>
<xsl:value-of select="@corresp"/>
<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="p/quote|l/quote">
<xsl:text>"</xsl:text>
<xsl:copy-of select="./node()"/>
<xsl:text>"</xsl:text>
</xsl:template>

</xsl:stylesheet>