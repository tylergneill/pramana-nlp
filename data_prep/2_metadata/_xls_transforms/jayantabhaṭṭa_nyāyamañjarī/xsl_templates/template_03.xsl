<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="sic" />

<xsl:template match="corr">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="unclear[@reason]">
<xsl:text>‥</xsl:text>
</xsl:template>

<xsl:template match="unclear[@resp='#nyāma-q']">
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="supplied">
<xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>