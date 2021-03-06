<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="unclear|label">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="q/lg|quote/lg">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="lg/l/q|lg/l/quote[not(@corresp)]">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="lg/l/quote[@corresp]">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>" (</xsl:text>
<xsl:value-of select="@corresp"/>
<xsl:text>)</xsl:text>
</xsl:template>

</xsl:stylesheet>