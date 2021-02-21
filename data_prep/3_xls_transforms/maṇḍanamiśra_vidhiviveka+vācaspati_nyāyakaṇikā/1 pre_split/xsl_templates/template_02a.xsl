<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//quote[@type='base-text']/p|//quote[@type='base-text']/lg">
<p>
<xsl:copy-of select="./@*"/>

<xsl:attribute name="pb_n">
<xsl:value-of select="preceding::pb[1]/@n"/>
</xsl:attribute>

<xsl:copy-of select="./node()"/>
</p>
</xsl:template>

</xsl:stylesheet>